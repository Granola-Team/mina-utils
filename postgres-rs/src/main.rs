use postgres::{Client, Error, NoTls, Row};

#[derive(Debug, Clone)]
pub struct BlockSummary {
    pub id: i32,
    pub parent_id: i32,
    pub height: i64,
    pub global_slot: i64,
    pub state_hash: String,
    pub parent_hash: String,
}

fn parse(row: Row) -> Option<BlockSummary> {
    row.get::<usize, Option<i32>>(1)
        .map(|parent_id| BlockSummary {
            id: row.get(0),
            parent_id, // genesis has NULL parent_id
            height: row.get(2),
            global_slot: row.get(3),
            state_hash: row.get(4),
            parent_hash: row.get(5),
        })
}

fn main() -> Result<(), Error> {
    let mut db =
        Client::connect("postgres://postgres:password@localhost:5432/archive", NoTls).unwrap();

    let rows = db
        .query(
            "
            SELECT
                id, parent_id, height, global_slot_since_genesis, state_hash, parent_hash
            FROM
                blocks",
            &[],
        )
        .unwrap();

    let block_infos: Vec<BlockSummary> = rows.into_iter().flat_map(parse).collect();

    for pid in 1..block_infos.len() as i32 {
        let children: Vec<BlockSummary> = block_infos
            .clone()
            .into_iter()
            .filter(|block_info| block_info.parent_id == pid)
            .collect();

        if !children.is_empty() {
            println!("----- Parent {pid} -----");
            println!("{:#?}", children);
        }
    }

    Ok(())
}
